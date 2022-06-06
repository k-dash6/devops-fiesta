import eel
import apps

if __name__ == '__main__':
    apps.create_cocktails()
    eel.init("web")
    eel.start("main_html.html", size=(1200, 800))