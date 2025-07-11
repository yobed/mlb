# Check out the website! [linescore.xyz](https://linescore.xyz/)


This was the python version to get the actual data.
> Still have to incorporate live data & recent data. (Total data is all games up to 2024)


---
# Python Version (down below)


# MLB Scores (vector search with a line score)

* Look up if a line score has ever been done before

* Cosine Similarity is just measuring the angle between two vectors, and those closer to 1 (meaning theta/angle is small) and close to eachother in magnitude and direction

## Example
```
$$$$$@### mlb % python main.py -v 0 0 5 0 0 1 1 0 1 2 3 -k 20

Target vector: [0, 0, 5, 0, 0, 1, 1, 0, 1, 2, 3]
                 game_id visteam hometeam                         line_score  similarity team_type
date                                                                                              
1921-09-05  PHA192109051     WS1      PHA  [0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1]    0.956365      home
1990-07-30  SDN199007300     ATL      SDN  [0, 0, 2, 0, 0, 0, 0, 0, 0, 1, 1]    0.956365       vis
1931-06-30  DET193106300     NYA      DET  [0, 0, 3, 0, 0, 1, 0, 0, 1, 0, 2]    0.927450       vis
2022-05-18  MIL202205180     ATL      MIL  [0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 1]    0.920263       vis
2000-04-25  FLO200004250     SFN      FLO  [0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 2]    0.918262       vis
1975-06-15  MIL197506151     CAL      MIL  [0, 0, 5, 0, 0, 0, 0, 0, 1, 0, 2]    0.912426       vis
1940-07-11  SLN194007110     NY1      SLN  [0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 2]    0.912426       vis
1990-09-15  ATL199009150     SDN      ATL  [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2]    0.909611       vis
2022-08-09  BOS202208090     ATL      BOS  [1, 0, 3, 0, 0, 1, 0, 1, 0, 1, 2]    0.909065       vis
1929-06-26  NY1192906260     BRO      NY1  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]    0.907959      home
1976-07-15  DET197607150     OAK      DET  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]    0.907959      home
2006-06-03  NYN200606032     SFN      NYN  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]    0.907959      home
1908-04-25  BSN190804250     PHI      BSN  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]    0.907959      home
1991-07-11  CHN199107110     HOU      CHN  [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 2]    0.907959       vis
1999-07-19  HOU199907190     CLE      HOU  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]    0.907959      home
2017-04-03  BAL201704030     TOR      BAL  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]    0.907959      home
2008-05-15  MIN200805150     TOR      MIN  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]    0.907959       vis
1978-05-27  SLN197805270     CHN      SLN  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]    0.907959       vis
1934-06-17  CHN193406172     BSN      CHN  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]    0.907959      home
2010-09-16  CLE201009160     ANA      CLE  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1]    0.907959      home
```


<img src="pics/heatmap.png" alt="Sentiment by Quarter" width="1000"/>

* I was at the [game](https://www.espn.com/mlb/game/_/gameId/270822201/rangers-orioles) (Away: 30 vs Home: 3) **bottom left in figure* See: 
... **It was the worst home loss in history of MLB**. 
