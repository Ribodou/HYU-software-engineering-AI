

# Connect 4I 

## Contributors 
**Name, Department, University, Email**

Marie Catharina Hartwell Pors, Business Analytics, Hanyang University/The Technical University of Denmark, [mariechpors@gmail.com](mailto:mariechpors@gmail.com)

Francesco Stefano Schirinzi, Computer Science, Hanyang University/ZHAW, [fschirinzi25@gmail.com](mailto:fschirinzi25@gmail.com)

Fabio Matteo Alfonso Motta, Engineering & Management, HYU/Pforzheim University, [fabiomotta98@gmail.com](mailto:fabiomotta98@gmail.com)

Bouillette Nicolas,,,

Ren Luca,,,

Robidou Lucas,,,


**Table of content** 

1. Introduction 
2. Datasets 
3. Methodology 
4. Evaluation & Analysis 
5. Related Work 
6. Conclusion 

 
 **I. Introduction** 

*   Motivation: Why are you doing this? 
*   What do you want to see at the end? 

Machine learning (ML) and Artificial Intelligence (AI) are becoming more and more advanced and are widely used in many different aspects. The applications of ML and AI are becoming a bigger part of our everyday lives. For example, when you’re typing on a smartphone and it gives you a suggestion on the next word based on the first part of a sentence, or when your camera auto adjusts its settings based on the image that it is currently seeing. Only a decade ago it was thought nearly impossible that a machine would be able to beat world champions in advanced strategy games such as Go, but now Go has now been convincingly defeated by AIs without human inputs. Reinforcement learning AIs can now start from random strategies playing against it self and achieve superhuman play tactics in less than 24 hours without any information from domain expects only the using the game rules (ref: [https://deepmind.com/research/case-studies/alphago-the-story-so-far](https://deepmind.com/research/case-studies/alphago-the-story-so-far)).  

As the world is opening up for the usefulness of ML and AI a need for more people understanding and working within this area is also essential. We are a group of students currently studying at Hanyang University that wants to extend our knowledge within this field. We are therefore building an AI playing Connect 4. This game is a turn-based game, which involves two players trying to connect four of their checkers in a row while preventing their opponent (the other player) from doing the same. This game will be playable through a web interface, and the outcomes will be saved on the server. Thus, we will be able to let the AI play against itself and train itself until a certain time has passed. Players will then be able to face the AI in the game.

The goal of this project is to obtain as good a Connect 4 AI as possible inside the timeframe and scope of this project to obtain as much experience working with multiple algorithms with different levels of difficulty as possible.

 

 

**II. Datasets** 

The data used for this project is obtained by letting the AIs play against itself over and over until a specified time runs out.

**III. Methodology** 



*   Explaining your choice of algorithms (methods) 
    *   Minimax first,
    *   then we try to implement Alpha-Zero algorithm
*   Explaining features or code (if any)  

**<span style="text-decoration:underline;">Minimax Algorithm</span>**

Minimax (MM) is a backtracking decision rule that is implemented for outcome optimization of decisional problems in various fields, such as decision theory, game theory, statistics, but also (and more importantly for us) in artificial intelligence. MM is based on the assumption that each player always plays optimally in his own interest and in perfect rationality (“_homo economicus”)_.

This algorithm is applicable to the connect 4 game because it is a turn-based two players zero-sum game. Zero sum game represents a situation in which each participant’s (player) gain or loss (in this case the score of the board state, and eventually the win or loss outcome) is exactly balanced by the losses or gains of the other participants (player). In “poor words”, the choices a player can make are directly dependant from the previous choice(s) of the other player, and vice versa.

In Minimax the two players are called maximizer and minimizer. The maximizer tries to get the highest score possible while the minimizer tries to do the opposite and get the lowest score possible.

The maximin value of a player is the highest value that the player can be sure to get without knowing the actions of the other players; equivalently, it is the lowest value the other players can force the player to receive when they know the player's action.

The minimax value of a player is the smallest value that the other players can force the player to receive, without knowing the player's actions; equivalently, it is the largest value the player can be sure to get when they know the actions of the other players.

The intrinsic perfect information of this game, allows to evaluate (assign a score) each possible board state and, more importantly, all possible consequent board states derived from all possible future states! If we represent this as a tree, the root would represent the first board state (only one piece from one player), and from there, for each turn (piece) we would generate seven children, each representing the board state for each column where the other player could drop the next piece. Each of these seven children, would have further seven children evaluating the possible moves derived from them. With this technique, the “computer” is able to “pre-play” all possible moves on the board and choose the score maximising strategy (path from root - current state-  to leaf representing winning the game) for each of the opponent’s moves. The superior computational power of the computer allows it to think ahead of all possible moves, and the opponent (human being) is left with the task of minimizing his loss.

**AlphaZero**

AlphaZero is a single system that can teach itself from scratch how to master the games of chess, shogi, and Go at superhuman level. AlphaZero was developed by DeepMind in 2017 and it gained a lot of attention because of the revolutionary results it obtained within the reinforcement learning (RL) area. In just 4 hours of training the AlphaZero AI was able to beat the former master AI in chess starting from a random strategy only playing against itself. The AlphaZero outperforms MiniMax in complex strategy games with shorter training period, because the AlphaZero system is better at aiming its search for the best possible strategy. 

The AlphaZero system contains three key components:



1. Deep convolutional neural network
2. Monte Carlo Tree Search (MCTS)
3. Reinforcement Learning (RL) to improve the performance of the neural network (NN)

Deep Convolutional Neural Network is a NN with convolutional layers that are used to detects filters in a network. The convolutional layers uses two main principles: translation invariance and locality (ref: [https://d2l.ai/chapter_convolutional-neural-networks/why-conv.html](https://d2l.ai/chapter_convolutional-neural-networks/why-conv.html)). The translation invariance focuses on the similarity of the objects regardless of the position and the locality focuses on the nearby region to see what is going on there instead of trying to look at the whole network. This reduces the number of parameters that has to be calculated drastically. ResNet is a popular way of making CNN and it is the one that we are going to use as well. ResNet is a deep convolutional residual neural network which includes a residual block. Plain NN should in theory get better when adding more hidden layers, but in practice we see that adding more layers will at some point start to make the solution different rather than better. ResNet tries to solve this problem by adding a residual block that makes networks strictly more expressive using nested functions. 

… more about the Connect 4 input, output, convolutional layer, residual block & the code …

Monte Carlo Tree Search is a heuristic search algorithm that search through the game tree in a smart and efficient way. The game tree of Connect 4 would have the current state of the game in the root and the branch would then have 7 possible moves that the AI could make, from the 7 possible moves the trees next branches would then have the opponents possible moves, and like that the tree branches on until the game ends in a win, lose or tie. 

 

**IV. Evaluation & Analysis** 



*   Graphs, tables, any statistics (if any)  

**V. Related Work (e.g., existing studies)** 



*   Tools, libraries, blogs, or any documentation that you have used to do this project.  

**VI. Conclusion:** 



* Discussion 

 
