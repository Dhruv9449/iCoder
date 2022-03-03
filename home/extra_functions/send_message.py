from django.contrib import messages


def send_message(request):
    if ('message' in request.session):
        message = request.session['message']
        messages.add_message(
            request, messages.INFO, message['message_text'], extra_tags=message['extra_tags'])
        del request.session['message']
