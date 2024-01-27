from django.shortcuts import render, redirect
from chat.models import Visitor, Chat
from chat.forms import LoginForm, NewChatForm


def index(request):
    if "visitor_id" not in request.session:
        return redirect("login")

    visitor = Visitor.objects.get(id=request.session["visitor_id"])

    context = {
        "visitor": visitor,
        "chats": Chat.objects.all(),
        "form": NewChatForm(),
    }

    if request.method == "POST":
        form = NewChatForm(request.POST)

        if form.is_valid():
            chat = Chat.objects.get_or_create(
                name=form.cleaned_data["name"],
            )[0]
            if chat.possible_to_add():
                chat.add_visitor(visitor)
                return redirect("chat", uuid=chat.uuid)
            else:
                context["error"] = "Chat cheio"
        else:
            context["error"] = "Dados inválidos para criação de chat"
            return redirect("home")

    return render(request, "index.html", context)


def login(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            visitor = Visitor.objects.get_or_create(name=request.POST["name"])[0]
            request.session["visitor_id"] = visitor.id
            return redirect("home")

    context = {"form": form}

    return render(request, "login.html", context)


def chat(request, uuid):
    chat = Chat.objects.get(uuid=uuid)
    visitor = Visitor.objects.get(id=request.session["visitor_id"])

    if visitor not in chat.visitors.all():
        if chat.possible_to_add():
            chat.add_visitor(visitor)
        else:
            return redirect("home")

    context = {
        "chat": chat,
        "room_uuid": uuid,
        "visitor": visitor,
    }

    return render(request, "chat.html", context)
