#include "snow.h"
#include "../dict/dict.h"
#define UNUSED(x) (void)(x)

void reset_attempts(list_attempts_t *attempts){
    attempts->nb_tries = 0;
    destroy_attempt(attempts->head);
    attempts->head = NULL;
}

describe(Dict) {
    list_attempts_t *attempts;
    int r_all_match_2_2_2[] = {2, 2, 2};
    int r_none_match_0_0_0[] = {0, 0, 0};
    int r_wrong_place_1_0_0[] = {1, 0, 0};
    int r_wrong_place_0_0_1[] = {0, 0, 1};
    int r_good_place_0_2_0[] = {0, 2, 0};

    before_each() {
        attempts = create_list_attempts(3);
        defer(destroy_list_attempts(attempts))
        ;
    }

    subdesc(constraints){
        it("Constraints struct initialization"){
            constraints_t *constraints = create_constraints(3);
            defer(destroy_constraints(constraints))
            ;asserteq(constraints->word_size, 3, "bad initialization")
            ;asserteq(constraints->global_forbidden_letters[25], false, "bad initialization")
            ;asserteq(constraints->global_forbidden_letters[0], false, "bad initialization")
            ;asserteq(constraints->emplacement_constraints->has_a_mandatory_letter, false, "bad initialization")
            ;asserteq(constraints->emplacement_constraints->forbidden_letters[25], false, "bad initialization")
            ;asserteq(constraints->word_constraint->is_exact_nb_occurrences_letters[25], false, "bad initialization")
            ;asserteq(constraints->word_constraint->min_nb_occurrences_letters[25], 0, "bad initialization")
            ;
        }
        it("compute_constraints_from_attempts"){
            append_attempt(attempts, "abc", r_all_match_2_2_2);
            constraints_t *constraints = compute_constraints_from_attempts(attempts);
            defer(destroy_constraints(constraints))
            ;asserteq(constraints->emplacement_constraints[2].has_a_mandatory_letter, true, " ")
            ;asserteq(constraints->emplacement_constraints[0].mandatory_letter, 'a', "'a' in first place")
            ;asserteq(constraints->emplacement_constraints[1].mandatory_letter, 'b', "'b' in second place")
            ;asserteq(constraints->emplacement_constraints[2].mandatory_letter, 'c', "'c' in third place")
            ;
            reset_attempts(attempts);
            destroy_constraints(constraints);
            append_attempt(attempts, "aba", r_wrong_place_1_0_0);
            constraints = compute_constraints_from_attempts(attempts);
            ;asserteq(constraints->global_forbidden_letters[1], true, "'b' cant be in the word")
            ;asserteq(constraints->word_constraint->is_exact_nb_occurrences_letters[0], true, "exact number of 'a' known")
            ;asserteq(constraints->word_constraint->min_nb_occurrences_letters[0], 1, "exactly one 'a'")
            ;asserteq(constraints->emplacement_constraints[0].forbidden_letters[0], true, "'a' cant be at the first place")
            ;asserteq(constraints->emplacement_constraints[1].forbidden_letters[0], false, "'a' can be at the second place")
            ;asserteq(constraints->emplacement_constraints[2].forbidden_letters[0], true, "'a' cant be at the last place")
            ;asserteq(constraints->emplacement_constraints[1].has_a_mandatory_letter, false,
                      "no known exact letter for second place. Even if only a word with 'a' in second place"
                      " can match previous constraints")
            ;
        }
    }

    subdesc(match){
        it("match with no attempt") {
            asserteq(is_matching_word_specific_attempts("hello", attempts), true, "any string should match with no attempt")
            ;asserteq(is_matching_word_specific_attempts("", attempts), true, "empty string should match with no attempt")
            ;
        }
        it("match with one attempt") {
            append_attempt(attempts, "abc", r_all_match_2_2_2);
            asserteq(is_matching_word_specific_attempts("abc", attempts), true, "should match")
            ;asserteq(is_matching_word_specific_attempts("aba", attempts), false, "should not match")
            ;asserteq(is_matching_word_specific_attempts("zzz", attempts), false, "should not match")
            ;
            reset_attempts(attempts);
            append_attempt(attempts, "abc", r_wrong_place_1_0_0);
            asserteq(is_matching_word_specific_attempts("azz", attempts), false,
                     "should not match bc if 'a' in first position is code 1 so 'a' can't be at this position")
            ;asserteq(is_matching_word_specific_attempts("zaz", attempts), true, "should match")
            ;asserteq(is_matching_word_specific_attempts("zza", attempts), true, "should match")
            ;asserteq(is_matching_word_specific_attempts("zzz", attempts), false, "should not match")
            ;asserteq(is_matching_word_specific_attempts("zba", attempts), false, "should not match")
            ;asserteq(is_matching_word_specific_attempts("zac", attempts), false, "should not match")
            ;
            reset_attempts(attempts);
            append_attempt(attempts, "aba", r_wrong_place_1_0_0);
            asserteq(is_matching_word_specific_attempts("zza", attempts), false,
                     "should not match bc we can deduce from aba->100 that the word has exactly one 'a'")
            ;asserteq(is_matching_word_specific_attempts("zaz", attempts), true, "should match")
            ;asserteq(is_matching_word_specific_attempts("zzz", attempts), false,
                      "should not match bc we can deduce from aba->100 that the word has exactly one 'a'")
            ;
            reset_attempts(attempts);
            append_attempt(attempts, "abc", r_none_match_0_0_0);
            asserteq(is_matching_word_specific_attempts("zzz", attempts), true, "should match")
            ;asserteq(is_matching_word_specific_attempts("azz", attempts), false, "should not match")
            ;asserteq(is_matching_word_specific_attempts("bzz", attempts), false,
                      "should not match, a letter with a zero code can't be part of the solution at any place")
            ;asserteq(is_matching_word_specific_attempts("czz", attempts), false, "should not match")
            ;
            reset_attempts(attempts);
            append_attempt(attempts, "aab", r_good_place_0_2_0);
            asserteq(is_matching_word_specific_attempts("zaz", attempts), true, "should match")
            ;asserteq(is_matching_word_specific_attempts("zaa", attempts), false,
                      "should not match bc we can deduce from aab->020 that the word has exactly one 'a'")
            ;
        }
        it("match with two attempts"){
            append_attempt(attempts, "abb", r_wrong_place_1_0_0);
            append_attempt(attempts, "bba", r_wrong_place_0_0_1);
            asserteq(is_matching_word_specific_attempts("zza", attempts), false, "should not match")
            ;asserteq(is_matching_word_specific_attempts("azz", attempts), false, "should not match")
            ;asserteq(is_matching_word_specific_attempts("zaz", attempts), true, "should match")
            ;asserteq(is_matching_word_specific_attempts("zzz", attempts), false, "should not match")
            ;
        }
    }
}





