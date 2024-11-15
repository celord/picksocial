import logging
from lib2to3.fixes.fix_input import context

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.transaction import commit
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from a_users.models import Profile
from .forms import InboxNewMessageForm
from .models import *


@login_required
def inbox_view(request, conversation_id=None):
    my_conversations = Conversation.objects.filter(participants=request.user)
    if conversation_id:
        conversation = get_object_or_404(my_conversations, id=conversation_id)
    else:
        conversation = None
    context = {
        "conversation": conversation,
        "my_conversations": my_conversations,
    }
    return render(request, "a_inbox/inbox.html", context)


def search_users(request):
    letters = request.GET.get("search_user")
    if request.htmx:
        if len(letters) > 0:
            profiles = Profile.objects.filter(realname__icontains=letters).exclude(
                user=request.user
            )
            users_id = profiles.values_list("user", flat=True)
            users = User.objects.filter(
                Q(username__icontains=letters) | Q(id__in=users_id)
            ).exclude(username=request.user.username)
            return render(request, "a_inbox/list_search_users.html", {"users": users})
        else:
            return HttpResponse("")
    else:
        raise Http404()


@login_required
def new_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    new_message_form = InboxNewMessageForm()
    if request.method == "POST":
        print(f"recipient: {recipient}")
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user

            my_conversations = request.user.conversations.all()
            for c in my_conversations:
                if recipient in c.participants.all():
                    print(f"conversation: {c}")
                    message.conversation = c
                    message.save()
                    c.lastmessage_created = timezone.now()
                    c.save()
                    return redirect("inbox", c.id)
            new_conversation = Conversation.objects.create()
            new_conversation.participants.add(request.user, recipient)
            new_conversation.save()
            message.conversation = new_conversation
            message.save()
            return redirect("inbox", new_conversation.id)

    context = {"recipient": recipient, "new_message_form": new_message_form}
    return render(request, "a_inbox/form_newmessage.html", context)


@login_required
def new_reply(request, conversation_id):
    new_message_form = InboxNewMessageForm()
    my_conversations = request.user.conversations.all()
    conversation = get_object_or_404(my_conversations, id=conversation_id)

    if request.method == "POST":
        form = InboxNewMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            conversation.lastmessage_created = timezone.now()
            conversation.save()
            conversation.lastmessage_created = timezone.now()
            conversation.save()
            return redirect("inbox", conversation.id)

    context = {"conversation": conversation, "new_message_form": new_message_form}
    return render(request, "a_inbox/form_newreply.html", context)
