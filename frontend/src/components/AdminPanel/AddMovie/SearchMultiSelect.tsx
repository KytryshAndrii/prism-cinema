import React, { useState } from 'react';
import { Autocomplete, Chip } from '@mui/material';
import { FormInput } from '../styles';
import { useSearchActorsQuery, useSearchDirectorsQuery, useSearchGenresQuery } from '../../../api/authApi';


type EntityType = 'actors' | 'directors' | 'genres';

type Props = {
  label: string;
  type: EntityType;
  selected: string[];
  setSelected: (v: string[]) => void;
};

export const SearchMultiSelect: React.FC<Props> = ({
  label,
  type,
  selected,
  setSelected,
}) => {
  const [phrase, setPhrase] = useState('');

  const actorQuery = useSearchActorsQuery(phrase, { skip: type !== 'actors' || !phrase });
  const directorQuery = useSearchDirectorsQuery(phrase, { skip: type !== 'directors' || !phrase });
  const genreQuery = useSearchGenresQuery(phrase, { skip: type !== 'genres' || !phrase });

  const data =
    type === 'actors'
      ? actorQuery.data
      : type === 'directors'
      ? directorQuery.data
      : genreQuery.data;

  const options = data?.map(e => e.name) ?? [];

  return (
    <Autocomplete
      multiple
      options={options}
      value={selected}
      filterSelectedOptions
      onChange={(_, value) => setSelected(value)}
      inputValue={phrase}
      onInputChange={(_, value) => setPhrase(value)}
      renderTags={(value, getTagProps) =>
        value.map((option, index) => (
          <Chip label={option} {...getTagProps({ index })} key={option} />
        ))
      }
      renderInput={params => (
        <FormInput {...params} label={label} />
      )}
    />
  );
};
