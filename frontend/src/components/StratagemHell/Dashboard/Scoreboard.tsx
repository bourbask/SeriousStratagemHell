import React from 'react';
import { Box, Typography } from '@mui/material';

interface ScoreboardProps {
    score: number;
    timeRemaining: number; // Time in seconds
}

const Scoreboard: React.FC<ScoreboardProps> = function ({ score, timeRemaining }) {
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'flex-start',
            }}
        >
            {/* Score Display */}
            <Typography
                variant="h4"
                sx={{ fontWeight: 'bold', mb: 1 }}
            >
                Score: {score}
            </Typography>

            {/* Time Remaining */}
            <Typography
                variant="h6"
                sx={{ color: timeRemaining < 10 ? 'red' : 'black' }}
            >
                Time Remaining: {timeRemaining}s
            </Typography>
        </Box>
    );
};

export default Scoreboard;
