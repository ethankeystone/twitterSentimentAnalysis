import CSVHandler
import PreProcess
import TwitterImport
import pandas as pd
import generalUtil
import os
from os import path

if __name__ == "main":
    args = parse_args()

    cwd = os.getcwd()
    if not os.path.exists('Twitter Data'):
        os.mkdir('Twitter Data')
    cwd = cwd + '\\Twitter Data\\'

    df = TwitterImport.generateDailyTwitterData('Elon Musk',50, cwd, accessCode)
