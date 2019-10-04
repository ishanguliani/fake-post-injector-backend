backend for chrome extension that performs fake post injection in Facebook timeline

# SCREENSHOTS 

### Screenshots of the chrome extension that this backend system is a part of:
The front end exists in a different repository https://github.com/ishanguliani/fake-post-chrome-extension

### This is how the fake chrome extension looks when installed
![This is how the fake chrome extension looks when installed](https://static.wixstatic.com/media/0a127f_55f0e01c9e464e9abf4332edaff024f8~mv2.png/v1/fill/w_824,h_442/Screen%20Shot%202019-02-19%20at%201.19.17%20PM.png
)

### These are sample injected fake posts

![](https://static.wixstatic.com/media/0a127f_a024a7ccd7ae4f24a3efe0f56f3cb1fb~mv2.png/v1/fill/w_1006,h_583/Screen%20Shot%202019-03-31%20at%208.17.58%20PM.png
)
![](https://static.wixstatic.com/media/0a127f_0e43a474762b40fbb87b85b059d8fa05~mv2.png/v1/fill/w_768,h_764/Screen%20Shot%202019-04-14%20at%2010.29.50%20PM.png
)

![](https://static.wixstatic.com/media/0a127f_740bc63871a04b4d8bd180395ba61cc1~mv2.png/v1/fill/w_772,h_812/Screen%20Shot%202019-04-14%20at%2010.30.06%20PM.png)

___


## Screenshots of the backend panel where you can upload your fake post models

![](https://static.wixstatic.com/media/0a127f_a51bb977d93d439fa6e7713bdb094430~mv2.png/v1/fill/w_956,h_754/Screen%20Shot%202019-05-24%20at%202.21.16%20AM.png
)

## Screenshots of the survey that the user takes after going through fake posts - this is all supported by the current python code

![](https://static.wixstatic.com/media/0a127f_82ed606accdd4db782acb4fe1c678782~mv2_d_2338_1378_s_2.png/v1/fill/w_2338,h_1378/Screen%20Shot%202019-05-27%20at%2012.37.16%20AM.png
)
![](https://static.wixstatic.com/media/0a127f_9a8d7d0ac8f44e058f0fc964664df92b~mv2_d_2334_1368_s_2.png/v1/fill/w_2334,h_1368/Screen%20Shot%202019-05-27%20at%2012.37.39%20AM.png
)
![](https://static.wixstatic.com/media/0a127f_7ce84bd1d0414ed1aec9104fe437899c~mv2_d_2338_1376_s_2.png/v1/fill/w_2338,h_1376/Screen%20Shot%202019-05-27%20at%2012.37.26%20AM.png
)
![](https://static.wixstatic.com/media/0a127f_55ba7509db8f4baebf438177c23ce1dc~mv2_d_2336_1376_s_2.png/v1/fill/w_2336,h_1376/Screen%20Shot%202019-05-27%20at%2012.38.16%20AM.png
)
![](https://static.wixstatic.com/media/0a127f_769460fffcc444a4a4419fc5412768ca~mv2_d_2340_1364_s_2.png/v1/fill/w_2340,h_1364/Screen%20Shot%202019-05-27%20at%2012.38.24%20AM.png
)



## REQUIREMENT
### To fire up the server have `python3` and `pipenv` installed.

## open terminal and cd to the project root directory 
### start virtual environment
`pipenv shell`
### install dependencies
`pipenv install`
### set up database locally
```
python3 manage.py makemigrations 
python3 manage.py migrate
```

### set up static files locally
`python3 manage.py collectstatic`
### start the server
`python3 manage.py runserver`

### Endpoints
```
Welcome screen: 127.0.0.1/
Admin panel: 127.0.0.1/admin
The survey: 127.0.0.1/surveyLinks/0/0
```
