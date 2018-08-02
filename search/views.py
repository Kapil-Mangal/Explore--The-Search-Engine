from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

from nltk.corpus import stopwords
from .models import loadNpyFile
import pandas as pd
import numpy as np 
import string
import random
from collections import Counter
from nltk.corpus import *
import webbrowser
import os

doclist=PlaintextCorpusReader('search/documents','.*')
fileids=doclist.fileids();
def index(request):
    
    return render(request,'search/index.html')

def detail(request):
    sentence=request.POST["query"]
    if(len(sentence)>0):
        qw=loadNpyFile.worddic[()]
        results=rank(sentence,qw)
        result=[]
        if results!="It doesn't exist":
            for i in results:
                result.append(fileids[i])
            
        else:    
            return HttpResponse(results)
        
        return render(request,'search/detail.html',{'result':result})
    else:
        return redirect("http://127.0.0.1:8000/search/")

def favorite(request,r):
    abs_path=os.path.abspath('.')
    filename = os.path.join(abs_path,'search/documents/'+r)
    webbrowser.open(filename)
    return HttpResponse("")

def search(searchsentence,worddic):
    
    try:
        searchsentence=searchsentence.lower()
        try:
            words=searchsentence.split(' ')
        except:
            words=list(words)
        enddic={}
        idfdic={}
        closdic={}

        realwords=[]
        for word in words:
            if word in list(worddic.keys()):
                realwords.append(word)
        words=realwords
        numwords=len(words)

        for word in words:
            for indpos in worddic[word]:
                index=indpos[0]
                amount=len(indpos[1])
                idfscore=indpos[2]
                enddic[index]=amount
                idfdic[index]=idfscore
                fullcount_order = sorted(enddic.items(), key=lambda x:x[1], reverse=True)
                fullidf_order = sorted(idfdic.items(), key=lambda x:x[1], reverse=True)
    
        combo = []
        alloptions = {k: worddic.get(k, None) for k in (words)}
        for worddex in list(alloptions.values()):
            for indexpos in worddex:
                for indexz in indexpos:
                    combo.append(indexz)
        comboindex = combo[::3]
        combocount = Counter(comboindex)
        for key in combocount:
            combocount[key] = combocount[key] / numwords
        combocount_order = sorted(combocount.items(), key=lambda x:x[1], reverse=True)       


        if len(words) > 1:
            x = []
            y = []
            for record in [worddic[z] for z in words]:
                for index in record:
                     x.append(index[0])
            for i in x:
                if x.count(i) > 1:
                    y.append(i)
            y = list(set(y))

            closedic = {}
            for wordbig in [worddic[x] for x in words]:
                for record in wordbig:
                    if record[0] in y:
                        index = record[0]
                        positions = record[1]
                        try:
                            closedic[index].append(positions)
                        except:
                            closedic[index] = []
                            closedic[index].append(positions)

            x = 0
            fdic = {}
            for index in y:
                csum = []
                for seqlist in closedic[index]:
                    while x > 0:
                        secondlist = seqlist
                        x = 0
                        sol = [1 for i in firstlist if i + 1 in secondlist]
                        csum.append(sol)
                        fsum = [item for sublist in csum for item in sublist]
                        fsum = sum(fsum)
                        fdic[index] = fsum
                        fdic_order = sorted(fdic.items(), key=lambda x:x[1], reverse=True)
                    while x == 0:
                        firstlist = seqlist
                        x = x + 1
        else:
            fdic_order = 0
        
        return(searchsentence,words,fullcount_order,combocount_order,fullidf_order,fdic_order)
    
    except:
        return("")

def rank(term,worddic):
    results=search(term,worddic)
    
    if(len(results)>0):
        num_score=results[2]
        per_score=results[3]
        tfscore = results[4]
        order_score = results[5]
        
        final_candidates = []
        
        try:
            first_candidates=[]

            for candidates in order_score:
                if candidates[1] > 1:
                    first_candidates.append(candidates[0])

            second_candidates = []

            for match_candidates in per_score:
                if match_candidates[1] == 1:
                    second_candidates.append(match_candidates[0])
                if match_candidates[1] == 1 and match_candidates[0] in first_candidates:
                    final_candidates.append(match_candidates[0])

            t3_order = first_candidates[0:3]
            for each in t3_order:
                if each not in final_candidates:
                    final_candidates.insert(len(final_candidates),each)

            final_candidates.insert(len(final_candidates),tfscore[0][0])
            final_candidates.insert(len(final_candidates),tfscore[1][0])

            t3_per = second_candidates[0:3]
            for each in t3_per:
                if each not in final_candidates:
                    final_candidates.insert(len(final_candidates),each)

            othertops = [num_score[0][0],per_score[0][0],tfscore[0][0],order_score[0][0]]
            for top in othertops:
                if top not in final_candidates:
                    final_candidates.insert(len(final_candidates),top)


        except:
            if(len(num_score)>2):
                othertops = [num_score[0][0],num_score[1][0],num_score[2][0],per_score[0][0],tfscore[0][0]]
            elif(len(num_score)>1):
                othertops = [num_score[0][0],num_score[1][0],per_score[0][0],tfscore[0][0]]
            else:
                othertops = [num_score[0][0],per_score[0][0],tfscore[0][0]]
            for top in othertops:
                if top not in final_candidates:
                    final_candidates.insert(len(final_candidates),top)
        return set(final_candidates)
    else:
        return "It doesn't exist"












#I am sure there is good in this situation.
#Today is a wonderful day, when everything moves smoothly and harmoniously.    
    
            
    





























    
























        
