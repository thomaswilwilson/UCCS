/* CS 123, Spring 2019
 * Basic game theory: Reducing Games
 *
 * Reduce games using iterative elimination.
 *
<<<<<<< HEAD
 * Thomas Wilson
=======
 * YOUR NAME
>>>>>>> 3a9d82334e6152aa31f503dfb37ebabf6a688bdf
 */

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
#include "reduce_game.h"

<<<<<<< HEAD
int compare_rows(game_t g, double* row1, double* row2) {
    /*
    *compare_rows: removes rows that can be stictly dominated.
    *inputs: 
    *   game_t: a game
    *   double* row1: the first row being checked
    *   double* row2: the second row being checked

    *returns: 
    *   1 if the second row dominates the first row
    *   0 if the first row dominates the second row
    *   3 if neither row dominates
    *   
    */
    int index1 = 0;
    int index2 = 0;

    for(int i = 0; i < g->m; i++) {

        if (row1[i] > row2[i]) {
            index1 ++;

        } else if (row1[i] < row2[i]) {
            index2 ++;
        }
    }

    if (index1 == g->m) {
        return 1;

    } else if (index2 == g->m) {
        return 0;

    } else {
        return 3;
    }
}


bool reduce_rows(game_t g, bool indicator) {
    /*
    *reduce_rows: removes rows that can be stictly dominated.
    *inputs: 
    *   game_t: a game
    *   bool indicator: Checks if there is a row removed
    *returns: 
    *   true if a row is removed
    *   false if there are no rows that can be removed
    */
    for(int i = 0; i < g->n; i++) {

        for(int j = 0; j < g->n; j++) {

            if (i != j){
                int row = compare_rows(g, g->player1[i], g->player1[j]);

                if (row == 1) {
                    remove_row_game(g, j);
                    return true;
                }

                if (row == 0) {
                    remove_row_game(g, i);
                    return true;
                }
            }
        }
    }
    return false;
}


int compare_cols(game_t g, int c, int c1) {
    /*
    *compare_cols: removes columns that can be stictly dominated.
    *inputs: 
    *   game_t: a game
    *   int c: the first column that is being checked
    *   int c1: the second column that is being checked

    *returns: 
    *   1 if the second column dominates the first column
    *   0 if the first column dominates the second column
    *   3 if nither column dominates
    *   
    */
    int index1 = 0;
    int index2 = 0;

    for (int i = 0; i < g -> n; i++) {

        if(g->player2[i][c] > g->player2[i][c1]) {
            index1 ++;

        } else if(g->player2[i][c] < g->player2[i][c1]) {
            index2 ++;
        }
    }

    if (index1 == g->n) {
        return 1;

    } else if (index2 == g->n) {
        return 0;

    } else {
        return 3;
    }
}


bool reduce_cols(game_t g, bool cindicator) {
    /*
    *reduce_cols: removes columns that can be stictly dominated.
    *inputs: 
    *   game_t: a game
    *   bool cindicator: Checks if there is a column removed
    *returns: 
    *   true if a column is removed
    *   false if there are no columnsthat can be removed
    */
    for(int i = 0; i < g->m; i++) {

        for(int j = 0; j < g->m; j++){

            if (i != j){
                int col = compare_cols(g, i, j);

                if (col == 1) {
                    remove_col_game(g, j);
                    return true;
                }

                if (col == 0) {
                    remove_col_game(g, i);
                    return true;
                }
            }
        }
    }
    return false;
}


void reduce(game_t g) {
    /* reduce: iteratively reduce rows and columns until no changes occur.
    *  game_t g: the game
    *
    *  Modifies the game, if there are rows or columns that can be reduced.
    */

    for(int i = 0; i < 2; i++) {

        bool indicator = true;
        bool cindicator = true;

        while (indicator == true && cindicator == true) {
            cindicator = reduce_cols(g, cindicator);
            indicator = reduce_rows(g, indicator);

        }
    }
}
=======
// YOUR AUXILIARY FUNCTIONS HERE

/* reduce: iteratively reduce rows and columns until no changes occur.
 *  game_t g: the game
 *
 *  Modifies the game, if there are rows or columns that can be reduced.
 */
void reduce(game_t g) {
  // YOUR CODE HERE
}

>>>>>>> 3a9d82334e6152aa31f503dfb37ebabf6a688bdf
