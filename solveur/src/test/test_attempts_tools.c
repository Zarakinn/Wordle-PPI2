#include "snow.h"
#include "../solver/attempts_tools.h"
#define UNUSED(x) (void)(x)

describe(attempts_tools) {
    list_attempts_t *attempts;
    int results_1[] = {11, 12, 13, 14, 15};
    int results_2[] = {2, 2, 2, 2, 2};

    before_each() {
        attempts = create_list_attempts();
    }
    after_each() {
        destroy_list_attempts(attempts);
    }

    it("creation") {
        asserteq(attempts->nb_tries, 0, "Empty list should have 0 elements");
        asserteq(attempts->head, NULL, "Empty list should have no first element");
    }
    it("insertion"){
        append_attempt(attempts, "apple", results_1);
        append_attempt(attempts, "melon", results_2);
        asserteq(attempts->nb_tries, 2, "List should have 2 elements");
    }
    it("access"){
        append_attempt(attempts, "apple", results_1);
        append_attempt(attempts, "melon", results_2);
        attempt_t *a1 = get_list_attempts(attempts, 0);
        attempt_t *a2 = get_list_attempts(attempts, 1);
        attempt_t *a3 = get_list_attempts(attempts, 2);
        attempt_t *a4 = get_list_attempts(attempts, -1);

        assertneq(a1, NULL, "First element should not be NULL");
        asserteq(a1->word, "apple", "First element should be 'apple'");
        asserteq(a1->results, results_1, "incorrect results for first element");

        assertneq(a2, NULL, "Second element should not be NULL");
        asserteq(a2->word, "melon", "Second element should be 'melon'");

        asserteq(a3, NULL, "Third element should be NULL");
        asserteq(a4, NULL, "-1 index element should be NULL");
    }

}