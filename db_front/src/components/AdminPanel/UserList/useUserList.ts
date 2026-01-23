import { useState } from 'react';
import {
  useGetUsersQuery,
  useDeleteUserMutation,
  useSearchUsersQuery,
} from '../../../api/authApi';
import type { tUser } from '../../../types/authTypes';

type tAlertState = {
  type: 'success' | 'error';
  message: string;
} | null;

export const useUserList = () => {
  const [searchPhrase, setSearchPhrase] = useState('');
  const [userToDelete, setUserToDelete] = useState<tUser | null>(null);
  const [alert, setAlert] = useState<tAlertState>(null);

  const { data: users, refetch } = useGetUsersQuery(undefined, {
    skip: !!searchPhrase,
  });

  const { data: searchedUsers, refetch: refetchSearch } = useSearchUsersQuery(searchPhrase, {
    skip: !searchPhrase,
  });

  const [deleteUser, { isLoading: isDeleting, isError }] = useDeleteUserMutation();

  const handleSearchChange = (value: string) => {
    setSearchPhrase(value);
  };

  const confirmDelete = async () => {
    if (!userToDelete || isDeleting) return;

    const result = await deleteUser(userToDelete.id);
    
    if (isError) {
      const status = (result.error as any)?.status;

      if (status === 404) {
        setAlert({
          type: 'error',
          message: 'User not found',
        });
      } else {
        setAlert({
          type: 'error',
          message: 'Server error. Please try again later.',
        });
      }

      return;
    } else {
      setAlert({
        type: 'success',
        message: 'User deleted successfully',
      });

      setUserToDelete(null);
      refetch();
      refetchSearch();
    }
  };

  const openDeleteModal = (user: tUser) => {
    setUserToDelete(user);
  };

  const cancelDelete = () => {
    setUserToDelete(null);
  };

  const closeAlert = () => {
    setAlert(null);
  };

  return {
    users: (searchPhrase ? searchedUsers : users) ?? [],
    searchPhrase,
    handleSearchChange,
    openDeleteModal,
    confirmDelete,
    cancelDelete,
    userToDelete,
    alert,
    closeAlert,
  };
};
