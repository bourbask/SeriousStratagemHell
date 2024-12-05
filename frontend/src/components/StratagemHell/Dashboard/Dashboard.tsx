import React, { FunctionComponent } from 'react';
import { Box } from '@mui/material';
import Scoreboard from './Scoreboard';
import NextComboPreview from './NextComboPreview';
import { PossibleKeys } from '../ComboObject/types';

interface DashboardProps {
    score: number;
    timeRemaining: number;
    nextCombo: PossibleKeys[];
}

const Dashboard: FunctionComponent<DashboardProps> = function ({
    score,
    timeRemaining,
    nextCombo,
}) {
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'row',
                justifyContent: 'space-between',
                alignItems: 'center',
                width: '100%',
                height: '100%',
                padding: 2,
            }}
        >
            {/* Scoreboard (Score + Time) */}
            <Scoreboard
                score={score}
                timeRemaining={timeRemaining}
            />

            {/* Next Combo Preview */}
            <NextComboPreview nextCombo={nextCombo} />
        </Box>
    );
};

export default Dashboard;
