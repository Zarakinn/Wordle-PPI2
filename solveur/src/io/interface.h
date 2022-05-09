#ifndef SOLVEUR_INTERFACE_H
#define SOLVEUR_INTERFACE_H

#include <stdbool.h>
/**
 * Affiche le message de bienvenue à l'utilsateur
 */
void print_hello();

/**
 * Demande à l'utilisateur de saisir le nombre de lettre du mot à deviner
 * @return le nombre de lettre
 */
int ask_for_word_length();

/**
 * Demande à l'utilisateur d'indiquer la solution sous la forme "00102"
 * @param result - le tableau entier qui est passée par référence puis modifiée par la méthode
 * @param tried_word - Le mot que le solveur propose
 */
void ask_for_answer(int result[], char *tried_word);

/**
 * Demande à l'utilisateur s'il veut rejouer
 * @return true si l'utilisateur veut rejouer, false sinon
 */
bool ask_for_replay();


#endif //SOLVEUR_INTERFACE_H
