import { useSelector } from 'react-redux';
import type { AppState } from '../../store/store';
import {
  useAddMovieToFavouritesMutation,
  useCheckIfMovieIsFavouriteMutation,
  useGetMovieDetailsQuery,
  useRemoveMovieFromFavouritesMutation,
} from '../../api/authApi';
import { useEffect, useState } from 'react';

export const useFilmDetailsRender = () => {
  const user = useSelector((state: AppState) => state.user);
  const { id, name } = useSelector((state: AppState) => state.film);

  const { data: details } = useGetMovieDetailsQuery(id!, { skip: !id });

  const [addToFav] = useAddMovieToFavouritesMutation();
  const [removeFromFav] = useRemoveMovieFromFavouritesMutation();
  const [checkFavourite] = useCheckIfMovieIsFavouriteMutation();

  const [isMovieFav, setIsMovieFav] = useState<boolean>(false);

  useEffect(() => {
    const fetchIsFav = async () => {
      if (user.id && id) {
        try {
          const result = await checkFavourite({
            user_id: user.id,
            movie_id: id,
          }).unwrap();
          setIsMovieFav(result.is_favorite);
        } catch (error) {
          throw new Error(`Failed to check favourite status: ${error}`);
        }
      }
    };

    fetchIsFav();
  }, []);

  const toggleLikeMovie = async () => {
    if (!user.id || !id) return;

    try {
      if (isMovieFav) {
        await removeFromFav({ user_id: user.id, movie_id: id });
      } else {
        await addToFav({ user_id: user.id, movie_id: id });
      }
      setIsMovieFav(!isMovieFav);
    } catch (error) {
      console.error('Failed to toggle favourite:', error);
    }
  };

  const formatYouTubeUrl = (url: string): string => {
    const match = url.match(/v=([^&]+)/);
    return match ? `https://www.youtube.com/embed/${match[1]}` : url;
  };

  const createImg = (img: string | null) => {
    return img ? `data:image/jpeg;base64,${img}` : undefined;
  };

  return {
    movieMeta: {
      id: id!,
      title: name,
      poster: createImg(details?.movie_poster || null),
      backdrop: createImg(details?.movie_preview_poster || null),
      trailerUrl: details?.trailer_url ? formatYouTubeUrl(details.trailer_url) : '',
      description: details?.description || '',
      cast: details?.actors || [],
      genres: details?.genres || [],
      directors: details?.directors || [],
      pg: details?.pg || '',
      release_date: details?.release_date || '',
      rating: details?.rating || '',
      isLiked: isMovieFav,
    },
    toggleLikeMovie,
  };
};
