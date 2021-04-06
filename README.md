# Questrade Portfolio Manager

## Introduction
Questrade is one of the investing brokers in Canada, and I have an account with them that I want to keep track of regularly. 

A jupyter notebook called 'Questrade Portfolio Manager' retrieves account information from Questrade API using a questrade wrapper called 'qtrade' and summarizes monthly activities, position changes and dividend income that I earned every month.

Whenever I am curious of how my investing account is doing, all I need to do is just run this notebook to see the overall performance. In terms of security, qtrade wrapper automatically refreshes a security token, so I don't have to log in to the website to get a new token everytime I run the notebook.

Below are a sample dataframe and visualizations I can create from the notebook.

## Breakdown of Holdings

<p align="center">
  <img width="600" height="600" src="https://user-images.githubusercontent.com/41933169/112911987-84be8400-90c4-11eb-94cf-b3c9836887f5.png">
</p>

## Monthly Dividend Income

<p align="center">
  <img width="800" height="500" src="https://user-images.githubusercontent.com/41933169/112912007-90aa4600-90c4-11eb-9868-7e1939e89af2.png">
</p>

## Holding Positions Summary

<p align="center">
  <img width="800" height="350" src="https://user-images.githubusercontent.com/41933169/112912042-a15abc00-90c4-11eb-8098-4c1e84b4b433.png">
</p>
