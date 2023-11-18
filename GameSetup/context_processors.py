# context_processors.py
# Get dynamic menu links so teachers can customize the links

from .models import GameSettings

def menu_links(request):

    #get teacher & class from session
    currentClassName = request.session.get('currentClassName')

    game_settings = GameSettings.objects.filter(className=currentClassName).first()

    if game_settings:
        # Fetching the individual fields from the game_settings instance
        user_guide = game_settings.userGuide
        electronic_book = game_settings.eBook
        class_slides = game_settings.classSlides
        video_lectures = game_settings.videoLectures

        # Return them in a dictionary
        return {
            'user_guide': user_guide,
            'electronic_book': electronic_book,
            'class_slides': class_slides,
            'video_lectures': video_lectures,
        }
    else:
        # Return an empty dictionary or some default values if GameSettings instance is not found
        return {}
