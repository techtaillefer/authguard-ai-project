"""FastAPI service for AuthGuard AI."""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from authguard import __version__
from authguard.model import score_event

app = FastAPI(
    title="AuthGuard AI",
    version=__version__,
    description="Defensive anomaly scoring for authentication telemetry.",
)


class AuthEvent(BaseModel):
    hour: int = Field(ge=0, le=23)
    failed_attempts: int = Field(ge=0, le=100)
    geo_distance_km: float = Field(ge=0, le=40075)
    device_trust_score: float = Field(ge=0, le=1)
    new_device: bool
    impossible_travel: bool
    ip_reputation_score: float = Field(ge=0, le=100)
    success: bool


class ScoreResponse(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    context_flags: list[str]
    model_version: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": __version__}


@app.post("/score", response_model=ScoreResponse)
def score(event: AuthEvent) -> dict:
    try:
        return score_event(event.model_dump())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
