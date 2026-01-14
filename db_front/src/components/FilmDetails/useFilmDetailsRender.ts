import { useSelector } from "react-redux";
import type { AppState } from "../../store/store";
import { useGetMovieDetailsQuery } from "../../api/authApi";

export const useFilmDetailsRender = () => {

  const { id, name, poster, preview_poster } = useSelector((state: AppState) => state.film);
  const {
    data: details,
  } = useGetMovieDetailsQuery(id!, { skip: !id });
// here need to implement logic for user if her has liked film

  const formatYouTubeUrl = (url: string): string => {
    const match = url.match(/v=([^&]+)/);
    return match ? `https://www.youtube.com/embed/${match[1]}` : url;
  }

  return {
    title: name,
    poster,
    backdrop: preview_poster,
    trailerUrl: details?.trailer_url ? formatYouTubeUrl(details.trailer_url) : "",
    description: details?.description || "",
    cast: details?.actors || [],
    genres: details?.genres || [],
    directors: details?.directors || [],
    pg: details?.pg || "",
    release_date: details?.release_date || "",
    rating: details?.rating || "",
    isLiked: true
  };
};
