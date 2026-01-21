import React from 'react';
import { Typography, IconButton } from '@mui/material';
import { SearchBar, MovieItem, MovieList, TrashBin } from './styles';
import { FormWrapper } from '../styles';

export const DeleteMovie: React.FC = () => {
  // Mock data (later from API)
  const movies = ['Kill Bill: Vol. 1', 'Kill the Irishman', 'Kill Me Three Times'];

  return (
    <FormWrapper>
      <Typography variant="h5">DELETE MOVIE</Typography>
      <SearchBar placeholder="Search movie..." />

      <MovieList>
        {movies.map(movie => (
          <MovieItem key={movie}>
            <Typography variant="body1">{movie}</Typography>
            <IconButton>
              <TrashBin />
            </IconButton>
          </MovieItem>
        ))}
      </MovieList>
    </FormWrapper>
  );
};
