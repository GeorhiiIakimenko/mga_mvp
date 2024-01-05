# analysis_app/views.py
from django.shortcuts import render, redirect
from .analysis import GoldMarketAnalyzer
from .forms import ExpertOpinionForm
from .models import ExpertOpinion
import openai
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings


# Ваше представление Django (например, analysis_page.html)
def analysis_page(request):
    analyzer = GoldMarketAnalyzer()
    analysis_results = analyzer.run_analysis()

    # Include expert opinion in the context
    context = {
        'analysis_results': analysis_results,
        'current_gold_price': analysis_results['current_gold_price'],
        'short_term_sma': analysis_results['short_term_sma'],
        'long_term_sma': analysis_results['long_term_sma'],
        # Добавьте другие значения по аналогии
    }

    return render(request, 'analysis_page.html', context)


def index(request):
    # Create an instance of the analyzer
    analyzer = GoldMarketAnalyzer()

    # Getting gold news data
    gold_news = analyzer.get_gold_news()

    # Predicting news sentiment
    news_sentiment = analyzer.analyze_news_sentiment(gold_news)

    # Getting gold price data
    current_gold_price = analyzer.get_gold_price()

    # Retrieve the latest expert opinion
    latest_expert_opinion = ExpertOpinion.objects.last()
    expert_opinion_text = latest_expert_opinion.opinion if latest_expert_opinion else "No expert opinion available"

    # Run the analysis
    analysis_results = analyzer.run_analysis()

    # Extracting relevant results
    prediction = analysis_results['prediction']
    next_day_prediction = analysis_results['next_day_prediction']
    next_week_prediction_trend = analysis_results['next_week_prediction_trend']
    overall_direction = analysis_results['overall_direction']
    gpt_response = analysis_results['gpt_response']

    context = {
        'current_gold_price': current_gold_price,
        'news_sentiment': news_sentiment,
        'prediction': prediction,
        'next_day_prediction': next_day_prediction,
        'next_week_prediction_trend': next_week_prediction_trend,
        'overall_direction': overall_direction,
        'gpt_response': gpt_response,
        'expert_opinion': expert_opinion_text,
        'short_term_sma': analysis_results['short_term_sma'],
        'long_term_sma': analysis_results['long_term_sma'],
        'macd': analysis_results['macd'],
        'next_week_prediction_price': analysis_results['next_week_prediction_price'],
        'weighted_conclusion': analysis_results['weighted_conclusion'],
    }

    return render(request, 'index.html', context)


def expert_opinion_form(request):
    if request.method == 'POST':
        form = ExpertOpinionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to a success page or any other page
    else:
        form = ExpertOpinionForm()

    return render(request, 'expert_opinion_form.html', {'form': form})


@csrf_exempt
@require_http_methods(["POST"])
def chat_with_assistant(request):
    data = json.loads(request.body)
    user_message = data.get("message")

    openai.api_key = settings.OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return JsonResponse({"response": response.choices[0].message["content"]})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
