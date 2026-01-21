import React, { useState } from 'react';
import { Typography } from '@mui/material';
import {
  FormWrapper,
  FormInput,
  TwoColumnRow,
  UploadButton,
  SaveButton,
  SearchBar,
} from '../styles';

export const EditMovie: React.FC = () => {
  const [form, setForm] = useState({
    title: '',
    rating: '',
    year: '',
    actors: '',
    directors: '',
    pg: '',
    language: '',
    licence: '',
    trailer: '',
    description: '',
  });

  const [poster, setPoster] = useState<File | null>(null);
  const [previewPoster, setPreviewPoster] = useState<File | null>(null);
  const [subtitles, setSubtitles] = useState<File | null>(null);

  const handleChange = (field: string, value: string) => {
    setForm(prev => ({ ...prev, [field]: value }));
  };
  const isValid = Object.values(form).every(Boolean) && poster && previewPoster && subtitles;

  return (
    <FormWrapper>
      <Typography variant="h5">EDIT MOVIE</Typography>

      <SearchBar placeholder="Search movie..." />

      <FormInput
        label="Title"
        fullWidth
        value={form.title}
        onChange={e => handleChange('title', e.target.value)}
      />

      <FormInput
        label="Movie rating"
        fullWidth
        value={form.rating}
        onChange={e => handleChange('rating', e.target.value)}
      />

      <FormInput
        label="Release year"
        fullWidth
        value={form.year}
        onChange={e => handleChange('year', e.target.value)}
      />

      <TwoColumnRow>
        <FormInput
          label="Actors"
          value={form.actors}
          onChange={e => handleChange('actors', e.target.value)}
        />
        <FormInput
          label="Directors"
          value={form.directors}
          onChange={e => handleChange('directors', e.target.value)}
        />
      </TwoColumnRow>

      <TwoColumnRow>
        <FormInput label="PG" value={form.pg} onChange={e => handleChange('pg', e.target.value)} />
        <FormInput
          label="Language"
          value={form.language}
          onChange={e => handleChange('language', e.target.value)}
        />
      </TwoColumnRow>

      <TwoColumnRow>
        <FormInput
          label="Licence"
          value={form.licence}
          onChange={e => handleChange('licence', e.target.value)}
        />

        <UploadButton>
          Poster Upload
          <input
            hidden
            type="file"
            accept="image/*"
            onChange={e => setPoster(e.target.files?.[0] || null)}
          />
        </UploadButton>
      </TwoColumnRow>

      <FormInput
        label="Trailer link"
        fullWidth
        value={form.trailer}
        onChange={e => handleChange('trailer', e.target.value)}
      />

      <FormInput
        multiline
        rows={3}
        label="Movie description"
        fullWidth
        value={form.description}
        onChange={e => handleChange('description', e.target.value)}
      />

      <TwoColumnRow>
        <UploadButton>
          Preview Poster
          <input
            hidden
            type="file"
            accept="image/*"
            onChange={e => setPreviewPoster(e.target.files?.[0] || null)}
          />
        </UploadButton>

        <UploadButton>
          Subtitles (JSON)
          <input
            hidden
            type="file"
            accept=".json"
            onChange={e => setSubtitles(e.target.files?.[0] || null)}
          />
        </UploadButton>
      </TwoColumnRow>

      <SaveButton disabled={!isValid}>SAVE</SaveButton>
    </FormWrapper>
  );
};
