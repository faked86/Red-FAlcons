from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...external.db.session import get_session
from ...external.oauth2.core import get_current_user
from ...external.oauth2.schemas import TokenData
from .core import (
    create_card,
    get_all_cards,
    get_single_card,
    get_sorted_card_list,
    delete_card,
)
from .schemas import CardIn, CardOut


cards_router = APIRouter(prefix="/cards", tags=["cards"])


@cards_router.get("/", summary="Get all cards.", response_model=list[CardOut])
async def get_all_cards_view(
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await get_all_cards(int(token_data.id), db)


@cards_router.get(
    "/geo", summary="Get cards sorted by geo.", response_model=list[CardOut | None]
)
async def get_geo_cards_view(
    latitude: float,
    longitude: float,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await get_sorted_card_list(int(token_data.id), db, latitude, longitude)


@cards_router.post(
    "/",
    summary="Create new card.",
    status_code=status.HTTP_201_CREATED,
    response_model=CardOut,
)
async def create_card_view(
    card: CardIn,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await create_card(card, int(token_data.id), db)


@cards_router.delete(
    "/{card_id}",
    summary="Delete card.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_card_view(
    card_id: int,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await delete_card(int(token_data.id), card_id, db)


@cards_router.get(
    "/{card_id}",
    summary="Get single card.",
    response_model=CardOut,
)
async def get_single_card_view(
    card_id: int,
    token_data: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
):
    return await get_single_card(int(token_data.id), card_id, db)
