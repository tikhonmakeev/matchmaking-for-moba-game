import logging

import api
from algorithm.matches_creation import compute_new_matches

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    NUMBER_OF_TESTS = 20
    # SERVER_URI = "http://0.0.0.0"
    SERVER_URI = "http://server"
    SERVER_PORT = "9000"

    for cur_test_ind in range(NUMBER_OF_TESTS):
        is_last_epoch = last_epoch_finished = False
        cur_epoch = "00000000-0000-0000-0000-000000000000"
        players_in_queue = []

        while not last_epoch_finished:
            get_response = api.get_request(SERVER_URI, SERVER_PORT, cur_test_ind, cur_epoch, logger)
            matches = compute_new_matches(get_response, players_in_queue, logger)
            post_response = api.post_matches(SERVER_URI, SERVER_PORT, cur_test_ind, cur_epoch, matches, logger)
            
            if post_response is None:
                break

            if is_last_epoch:
                last_epoch_finished = True
            elif post_response.json()["is_last_epoch"] is True:
                is_last_epoch = True

            cur_epoch = post_response.json()["new_epoch"] if post_response.json()["new_epoch"] else None