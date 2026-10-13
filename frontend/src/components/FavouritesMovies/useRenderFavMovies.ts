import { useDispatch, useSelector } from 'react-redux';
import {
  useGetUserFavouriteMoviesQuery,
  useRemoveMovieFromFavouritesMutation,
} from '../../api/authApi';
import type { AppState } from '../../store/store';
import { useNavigate } from 'react-router-dom';
import { setFilm } from '../../store/filmSlice';
import type { tFilmMetaData } from '../MainPage/types';

export const useRenderFavMovies = () => {
  const userId = useSelector((state: AppState) => state.user.id);
  const [removeFromFav] = useRemoveMovieFromFavouritesMutation();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const { data, isLoading, isError, refetch } = useGetUserFavouriteMoviesQuery(userId!, {
    skip: !userId,
    refetchOnMountOrArgChange: true,
  });

  const handleFilmClick = (film: tFilmMetaData) => {
    dispatch(setFilm({ id: film.id, name: film.title }));
    navigate('/film_entity');
  };

  const handleRemoveFromFav = async (movieId: string) => {
    try {
      await removeFromFav({ user_id: userId!, movie_id: movieId }).unwrap();
      await refetch();
    } catch (err) {
      console.error('Failed to remove from favourites', err);
    }
  };

  return {
    films: (data || []).map(movie => ({
      id: movie.movie_id,
      title: movie.movie_name,
      imageUrl: `data:image/jpeg;base64,${movie.movie_poster}`,
    })),
    isLoading,
    isError,
    handleFilmClick,
    handleRemoveFromFav,
  };
};
