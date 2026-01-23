import React, { useState } from 'react';
import { Alert, CircularProgress } from '@mui/material';

import {
  useSearchActorsQuery,
  useSearchDirectorsQuery,
  useSearchGenresQuery,
} from '../../../api/authApi';

import {
  Wrapper,
  Title,
  FormInput,
  TwoColumnRow,
  UploadButton,
  SaveButton,
  StyledAutocomplete,
} from './styles';

import { useAddMovie } from './useAddMovie';
import type { tSearchEntityResponse } from '../../../types/authTypes';

export const AddMovie: React.FC = () => {
  const {
    form,
    handleChange,

    actorIds,
    setActorIds,
    directorIds,
    setDirectorIds,
    genreIds,
    setGenreIds,

    setPoster,
    setPreviewPoster,
    setSubtitles,

    saveMovie,
    alert,
    closeAlert,
    isLoading,
  } = useAddMovie();

  const [actorSearch, setActorSearch] = useState('');
  const [directorSearch, setDirectorSearch] = useState('');
  const [genreSearch, setGenreSearch] = useState('');

  const { data: actors = [] } = useSearchActorsQuery(actorSearch, {
    skip: actorSearch.length < 1,
  });

  const { data: directors = [] } = useSearchDirectorsQuery(directorSearch, {
    skip: directorSearch.length < 1,
  });

  const { data: genres = [] } = useSearchGenresQuery(genreSearch, {
    skip: genreSearch.length < 1,
  });

  // ===========================
  // Helpers — map IDs -> objects
  // ===========================

  const selectedActors = actorIds
    .map(id => actors.find(a => a.id === id))
    .filter((x): x is tSearchEntityResponse => Boolean(x));

  const selectedDirectors = directorIds
    .map(id => directors.find(d => d.id === id))
    .filter((x): x is tSearchEntityResponse => Boolean(x));

  const selectedGenres = genreIds
    .map(id => genres.find(g => g.id === id))
    .filter((x): x is tSearchEntityResponse => Boolean(x));

  // ===========================
  // UI
  // ===========================

  return (
    <Wrapper>
      <Title>ADD MOVIE</Title>

      {alert && (
        <Alert severity={alert.type} onClose={closeAlert}>
          {alert.message}
        </Alert>
      )}

      <FormInput
        label="Title"
        value={form.title}
        onChange={e => handleChange('title', e.target.value)}
      />

      <TwoColumnRow>
        <FormInput
          label="Rating"
          value={form.rating}
          onChange={e => handleChange('rating', e.target.value)}
        />

        <FormInput
          type="date"
          label="Release Date"
          InputLabelProps={{ shrink: true }}
          value={form.year}
          onChange={e => handleChange('year', e.target.value)}
        />
      </TwoColumnRow>

      <TwoColumnRow>
        <FormInput
          label="PG"
          value={form.pg}
          onChange={e => handleChange('pg', e.target.value)}
        />

        <FormInput
          label="Language (ISO)"
          value={form.language}
          onChange={e => handleChange('language', e.target.value)}
        />
      </TwoColumnRow>

      {/* ACTORS */}
      <StyledAutocomplete<tSearchEntityResponse>
        multiple
        options={actors}
        value={selectedActors}
        onInputChange={(_, v) => setActorSearch(v)}
        onChange={(_, v) => setActorIds(v.map(x => x.id))}
        getOptionLabel={o => o.name}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        renderInput={params => <FormInput {...params} label="Actors" />}
      />

      {/* DIRECTORS */}
      <StyledAutocomplete<tSearchEntityResponse>
        multiple
        options={directors}
        value={selectedDirectors}
        onInputChange={(_, v) => setDirectorSearch(v)}
        onChange={(_, v) => setDirectorIds(v.map(x => x.id))}
        getOptionLabel={o => o.name}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        renderInput={params => <FormInput {...params} label="Directors" />}
      />

      {/* GENRES */}
      <StyledAutocomplete<tSearchEntityResponse>
        multiple
        options={genres}
        value={selectedGenres}
        onInputChange={(_, v) => setGenreSearch(v)}
        onChange={(_, v) => setGenreIds(v.map(x => x.id))}
        getOptionLabel={o => o.name}
        isOptionEqualToValue={(a, b) => a.id === b.id}
        renderInput={params => <FormInput {...params} label="Genres" />}
      />

      <TwoColumnRow>
        <FormInput
          label="License ID"
          value={form.licence}
          onChange={e => handleChange('licence', e.target.value)}
        />

        <UploadButton component="label">
          POSTER
          <input
            hidden
            type="file"
            accept="image/*"
            onChange={e => setPoster(e.target.files?.[0] || null)}
          />
        </UploadButton>
      </TwoColumnRow>

      <FormInput
        label="Trailer Link"
        value={form.trailer}
        onChange={e => handleChange('trailer', e.target.value)}
      />

      <FormInput
        multiline
        rows={4}
        label="Description"
        value={form.description}
        onChange={e => handleChange('description', e.target.value)}
      />

      <TwoColumnRow>
        <UploadButton component="label">
          PREVIEW POSTER
          <input
            hidden
            type="file"
            accept="image/*"
            onChange={e => setPreviewPoster(e.target.files?.[0] || null)}
          />
        </UploadButton>

        <UploadButton component="label">
          SUBTITLES JSON
          <input
            hidden
            type="file"
            accept=".json"
            onChange={e => setSubtitles(e.target.files?.[0] || null)}
          />
        </UploadButton>
      </TwoColumnRow>

      <SaveButton disabled={isLoading} onClick={saveMovie}>
        {isLoading ? <CircularProgress size={22} /> : 'ADD MOVIE'}
      </SaveButton>
    </Wrapper>
  );
};
