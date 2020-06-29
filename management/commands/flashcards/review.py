from typing import List, Tuple
from decimal import Decimal as Dec

from ..util import assert_arguments
from ...session import Session
from ...query import Query
from .primitives import get_flashcard_deck_id


def update_e_factor(e_factor: Dec, score: int) -> Dec:
    inverse_score = 5 - score
    shift = Dec(0.1) - \
        (inverse_score * (Dec(0.08) + (inverse_score * Dec(0.02))))
    e_factor_prime = e_factor + shift

    return max(Dec(1.3), e_factor_prime)


def update_review_interval(
    pseudo_review_count, review_interval: int, e_factor: Dec,
) -> Tuple[int, int]:
    if e_factor < 3:
        return 1, 1

    if pseudo_review_count == 1:
        return 2, 6

    return (pseudo_review_count + 1), e_factor * review_interval


def update_card(session: Session, flashcard_id: int, score: int):
    review_definition = Query(
        session,
        '''select review_count, pseudo_review_count, review_interval, e_factor
        from flashcard_reviews where flashcard_id = %s
        order by review_time desc limit 1;''',
        (flashcard_id,),
    ).one_or_none()
    if review_definition is None:
        review_count = 1
        pseudo_review_count = 1
        review_interval = 1
        e_factor = 2.5 
    else:
        review_count, pseudo_review_count, review_interval, e_factor = \
            review_definition

    new_e_factor = update_e_factor(e_factor, score)
    new_pseudo_review_count, new_review_interval = \
        update_review_interval(pseudo_review_count,
                               review_interval,
                               new_e_factor)
    Query(
        session,
        '''insert into flashcard_reviews
        (flashcard_id, review_count,
         pseudo_review_count, review_interval,
         e_factor)
        values
        (%s, %s, %s, %s)
        returning (id);''',
        (flashcard_id, review_count + 1,
         new_pseudo_review_count, new_review_interval,
         new_e_factor),
    ).run()


def review_flashcard(session: Session, arguments: List[str]):
    deck_identifier, = assert_arguments(arguments, 1)
    deck_id, _ = get_flashcard_deck_id(session, deck_identifier)
    flashcard_id, front, back = Query(session, """
        with (
            select flashcard_id, max(review_time) from flashcard_reviews
            group by flashcard_id
        ) as cte_1,
        (select flashcard_id,
         review_time
         review_time + (review_interval * INTERVAL '1 day') as next_review
         from flashcard_reviews
         where flashcard_id, review_time in cte_1
        ) as cte_2
        select flashcards.id, front, back
        from flashcards
        left join cte_2
        on flashcards.id = cte_2.flashcard_id
        where flashcards.deck_id = %s
        order by cte_2.next_review
        limit 1;
    """, (deck_id,)).one()
    print(front)


def print_response_codes(session: Session, arguments: List[str]):
    print('''
    (5) - correct instantly
    (4) - correct after a moment
    (3) - correct after effort
    (2) - incorrect, correct was easy to recall
    (1) - incorrect, correct was recalled
    (0) - completely blank/wrong
    ''')
