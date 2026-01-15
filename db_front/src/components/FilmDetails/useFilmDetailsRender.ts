import { useSelector } from "react-redux";
import type { AppState } from "../../store/store";
import { useGetMovieDetailsQuery } from "../../api/authApi";

export const useFilmDetailsRender = () => {

  const { id, name} = useSelector((state: AppState) => state.film);
  const {
    data: details,
  } = useGetMovieDetailsQuery(id!, { skip: !id });
// here need to implement logic for user if her has liked film

  const formatYouTubeUrl = (url: string): string => {
    const match = url.match(/v=([^&]+)/);
    return match ? `https://www.youtube.com/embed/${match[1]}` : url;
  }

  const createImg = (img: string | null) => {
    if (img) return `data:image/jpeg;base64,${img}`
  }

  return {
    title: name,
    poster: createImg(details?.movie_poster || null),
    backdrop: createImg(details?.movie_preview_poster || null),
    trailerUrl: details?.trailer_url ? formatYouTubeUrl(details.trailer_url) : "",
    description: details?.description || "",
    cast: details?.actors || [],
    genres: details?.genres || [],
    directors: details?.directors || [],
    pg: details?.pg || "",
    release_date: details?.release_date || "",
    rating: details?.rating || "",
    isLiked: false
  };
};
