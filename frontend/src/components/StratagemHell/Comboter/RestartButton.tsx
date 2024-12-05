import React, { FunctionComponent } from 'react';
import { Tooltip, Button } from '@mui/material';

const RestartButton: FunctionComponent<{ onClick: () => void }> = function ({ onClick }) {
    return (
        <Tooltip title="Or press ⏎">
            <Button
                variant="contained"
                color="primary"
                onClick={onClick}
                sx={{ fontSize: '1.2rem', padding: '10px 20px' }}
            >
                Restart
            </Button>
        </Tooltip>
    );
};

export default RestartButton;
