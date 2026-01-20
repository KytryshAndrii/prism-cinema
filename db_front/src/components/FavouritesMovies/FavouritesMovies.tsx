import React from 'react';
import {
  Container,
  FilmsGrid,
  FilmCard,
  FilmImage,
  FilmInfo,
  FilmTitle,
  LikeButtonOverlay,
  HeartLikeIcon,
} from '../MainPage/styles';
import { useRenderFavMovies } from './useRenderFavMovies';
import { CircularProgress, Typography } from '@mui/material';

const FavouritesMovies: React.FC = () => {
  const { films, isLoading, isError, handleRemoveFromFav, handleFilmClick } = useRenderFavMovies();

  return (
    <Container>
      {isLoading && <CircularProgress />}
      {isError && <Typography color="error">Failed to load favourite movies.</Typography>}

      <FilmsGrid>
        {films.map(film => (
          <FilmCard key={film.id}>
            <LikeButtonOverlay onClick={() => handleRemoveFromFav(film.id)}>
              <HeartLikeIcon />
            </LikeButtonOverlay>
            <FilmImage src={film.imageUrl} alt={film.title} onClick={() => handleFilmClick(film)} />
            <FilmInfo>
              <FilmTitle>{film.title}</FilmTitle>
            </FilmInfo>
          </FilmCard>
        ))}
      </FilmsGrid>
    </Container>
  );
};

export default FavouritesMovies;
