"""Engine types for topic planning and generation requests."""

from pydantic import BaseModel, Field


class PlannedTopic(BaseModel):
    """A scheduled topic in the content plan."""

    topic: str = Field(description="Working topic title")
    slug: str = Field(description="Target URL slug")
    category: str = Field(description="Category slug")
    target_keywords: list[str] = Field(default_factory=list, description="Target search queries")
    target_date: str = Field(description="Scheduled publishing date YYYY-MM-DD")
    rationale: str = Field(default="", description="Strategic reason for this topic")


class ContentPlan(BaseModel):
    """Multi-week content publishing plan."""

    brand_name: str
    start_date: str
    end_date: str
    cadence_per_week: float
    topics: list[PlannedTopic] = Field(default_factory=list)


class GenerationRequest(BaseModel):
    """Input parameters for a blog post generation run."""

    topic: str
    category: str
    target_date: str | None = None
    target_keywords: list[str] = Field(default_factory=list)
    image_override: str | None = None
    used_images: list[str] = Field(default_factory=list)


class ExistingPostSummary(BaseModel):
    """Summary of an existing post parsed from posts.ts."""

    slug: str
    image: str = ""
    category: str = ""
    titles: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)


class StrikingKeyword(BaseModel):
    """Search query ranking in striking distance."""

    query: str
    position: float = 0.0
    impressions: int = 0
    clicks: int = 0
