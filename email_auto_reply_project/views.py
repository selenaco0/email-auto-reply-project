import json
from . import views_util, model_util
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

def home(request): #GET
    # return render(request, 'auto_reply.html')
    all_inquiry_questions = model_util.retrieve_all_inquiry_questions()
    return render(request, 'auto_reply.html', {'inquiry_questions': all_inquiry_questions})

@csrf_exempt
def auto_reply_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email_content = data.get("content", "")

            reply_message, questions = views_util.process_email_for_auto_reply(email_content)

            return JsonResponse({
                'reply': reply_message,
                'questions': questions,
                'status': 'success'
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format', 'status': 'failure'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed', 'status': 'failure'}, status=405)
