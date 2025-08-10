%Лабараторная работа №2 по дисциплине ЛОИС
%Выполнена студентом группы 321701 Климков Марат Петрович
%Программа содержит описание предикатов, позволяющих решить задачу 
%про человека, капусту, козу и волка
%чтобы капуста не оставалась с козой, а коза с волком без человека
%31.05.2025

startState(state(left, left, left, left)).

goalState(state(right, right, right, right)).

opposite(left, right).
opposite(right, left).

safeState(state(H,G,W,C)) :-
    \+ (G == C, H\==G),
    \+ (G == W, H\==G).

move(state(H,G,W,C), state(H1,G1,W1,C1)):-
    opposite(H,H1),
    (
        G1 = H1, W1 = W, C1 = C
        ;
        W1 = H1, G1 = G, C1 = C
        ;
        C1 = H1, G1 = G, W1 = W
        ;
        G1 = G, W1 = W, C1 = C
    ).

solvePath([Current | Path], _, Solution) :-
    goalState(Current),
    Solution = [Current | Path].

solvePath([Current | Path], Visited, Solution) :-
    move(Current, Next),
    \+ member(Next, Visited),
    safeState(Next),
    solvePath([Next, Current | Path], [Current | Visited], Solution).

solve(Solution) :-
    startState(Start),
    solvePath([Start], [], ReversedSolution),
    reverse(ReversedSolution, Solution).

describeSide(Side, H, G, W, C) :-
    (H == Side -> write('человек '); true),
    (G == Side -> write('коза '); true),
    (W == Side -> write('волк '); true),
    (C == Side -> write('капуста '); true).

describeState(state(H, G, W, C)) :-
    write('Левый берег: '), describeSide(left, H, G, W, C),
    write(' | Правый берег: '), describeSide(right, H, G, W, C), nl.

writeSolutionSteps([]).

writeSolutionSteps([Step | Rest]) :-
    describeState(Step),
    writeSolutionSteps(Rest).

writeSolutions([]).

writeSolutions([Solution | Rest]) :-
    write('Решение: '), nl,
    writeSolutionSteps(Solution),
    writeSolutions(Rest).

getSolution :-
    findall(S, solve(S), Solutions),
    sort(Solutions,UniqueSolutions),
    writeSolutions(UniqueSolutions),

