import { useGetMoviesQuery } from "../../api/authApi";

export const useMainPageFilmsRender = () => {
  const { data, isLoading, isError } = useGetMoviesQuery();

  const films = (data || []).map((movie) => ({
    id: movie.movie_id,
    title: movie.movie_name,
    imageUrl: `data:image/jpeg;base64,${movie.movie_poster}`,
    previewImg: `data:image/jpeg;base64,${movie.movie_preview_poster}`
  }));

  return {
    films,
    isLoading,
    isError,
  };
};
