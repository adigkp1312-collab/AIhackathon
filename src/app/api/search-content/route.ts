import { NextRequest, NextResponse } from "next/server";
import { searchYouTube, searchNPTEL } from "@/lib/youtube";
import type { ContentResource } from "@/types";

export const dynamic = "force-dynamic";

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const q = searchParams.get("q");
    const lang = searchParams.get("lang") || "en";
    const max = parseInt(searchParams.get("max") || "5", 10);

    if (!q) {
      return NextResponse.json(
        { error: "Search query (q) is required" },
        { status: 400 }
      );
    }

    // Fetch YouTube and NPTEL results in parallel
    const [youtubeResults, nptelResults] = await Promise.all([
      searchYouTube(q, lang, max).catch(() => []),
      Promise.resolve(searchNPTEL(q)),
    ]);

    // Combine and sort by rating (descending), treating missing ratings as 0
    const combined: ContentResource[] = [...youtubeResults, ...nptelResults];
    combined.sort((a, b) => (b.rating ?? 0) - (a.rating ?? 0));

    return NextResponse.json({ results: combined });
  } catch (error) {
    console.error("Error searching content:", error);
    return NextResponse.json(
      { error: "Failed to search content" },
      { status: 500 }
    );
  }
}
