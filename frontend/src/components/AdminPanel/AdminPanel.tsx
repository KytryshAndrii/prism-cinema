import React, { useState } from 'react';
import { DeleteMovie } from './DeleteMovie/DeleteMovie';
import { EditMovie } from './EditMovie/EditMovie';
import { AddMovie } from './AddMovie/AddMovie';
import { UserList } from './UserList/UserList';
import { PanelWrapper, LeftPanel, RightPanel, ToggleButton, ToggleContainer } from './styles';

const AdminPanel: React.FC = () => {
  const [activePanel, setActivePanel] = useState<'delete' | 'edit' | 'add'>('delete');

  return (
    <PanelWrapper>
      <LeftPanel>
        <ToggleContainer>
          <ToggleButton onClick={() => setActivePanel('edit')} active={activePanel === 'edit'}>
            EDIT MOVIE
          </ToggleButton>
          <ToggleButton onClick={() => setActivePanel('delete')} active={activePanel === 'delete'}>
            DELETE MOVIE
          </ToggleButton>
          <ToggleButton onClick={() => setActivePanel('add')} active={activePanel === 'add'}>
            ADD MOVIE
          </ToggleButton>
        </ToggleContainer>

        {activePanel === 'edit' && <EditMovie />}
        {activePanel === 'delete' && <DeleteMovie />}
        {activePanel === 'add' && <AddMovie />}
      </LeftPanel>

      <RightPanel>
        <UserList />
      </RightPanel>
    </PanelWrapper>
  );
};

export default AdminPanel;
