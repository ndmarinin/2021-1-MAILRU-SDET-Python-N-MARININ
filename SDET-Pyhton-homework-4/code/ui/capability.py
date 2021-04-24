from selenium import webdriver
import os


def capability_select(device_os, download_dir):
    capability = {"platformName": "Android",
                      "platformVersion": "8.1",
                      "automationName": "Appium",
                      "appPackage": "ru.mail.search.electroscope",
                      "appActivity": ".ui.activity.AssistantActivity",
                      "app": os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                          '../stuff/Marussia_v1.39.1.apk')
                                             ),
                      "orientation": "PORTRAIT"
                      }
    return capability