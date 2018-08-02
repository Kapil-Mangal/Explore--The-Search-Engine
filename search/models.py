from django.db import models
import numpy as np

class loadNpyFile(models.Model):
    worddic=np.load('search/worddic_999.npy')
