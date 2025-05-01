from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, Message
from .forms import MessageForm

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Verify user has access to this room
    if request.user not in [room.user, room.counselor]:
        return redirect('home')
    
    messages = room.messages.all()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.sender = request.user
            message.save()
            return redirect('chat:room', room_id=room.id)
    else:
        form = MessageForm()
    
    return render(request, 'chat/chat_room.html', {
        'room': room,
        'messages': messages,
        'form': form,
        'other_user': room.counselor if request.user == room.user else room.user,
    })

@login_required
def chat_history(request):
    if request.user.is_counselor:
        rooms = ChatRoom.objects.filter(counselor=request.user)
    else:
        rooms = ChatRoom.objects.filter(user=request.user)
    
    return render(request, 'chat/chat_history.html', {'rooms': rooms})