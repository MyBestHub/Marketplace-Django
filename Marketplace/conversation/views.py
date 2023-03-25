from django.shortcuts import render, get_object_or_404, redirect
from item.models import Item
from .models import Conversation
from .forms import ConversationMessageForm
from django.contrib.auth.decorators import login_required  #require to be logged to access the content

@login_required
def new_conversation(request, item_pk):     #when we click contact seller, it be sent to this page
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:   #So the owner cant visit this page
        return redirect('dashboard:index')
    
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user.id]) #check if the Id is one of the members.
    
    if conversations:
        return redirect('conversation:detail', pk=conversation.first().id)  #to be sent to the conversation page

    if request.method == 'POST':                  #check if form is submitted
        form = ConversationMessageForm(request.POST)

        if form.is_valid():                                         # check if form is valid and filled correctly
            conversation = Conversation.objects.create(item=item)  
            conversation.members.add(request.user)            #add owner and user to members list
            conversation.members.add(item.created_by)         #add owner and user to members list
            conversation.save()

            conversation_message = form.save(commit=False)    #create convo message, commit False so no error from database
            conversation_message.conversation = conversation  #reference to the convo
            conversation_message.created_by = request.user    #who created it
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)        #redirect to item
    else:
        form = ConversationMessageForm()                  #Empty form if no Post request

    return render(request, 'conversation/new.html', {
            'form': form
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations
    })


@login_required
def detail(request, pk):   #this pk will be used for the convo, not items
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':  #send a message when we click "Respond or Send from detail.html" to respond to the messages
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save() #to update the modified date of the conversation

            return redirect('conversation:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail.html', {
        'conversation': conversation,
        'form': form
    })



