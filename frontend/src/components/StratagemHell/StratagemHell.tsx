import React, { FunctionComponent } from 'react';
import { Box, Card } from '@mui/material';
import Dashboard from './Dashboard/Dashboard';
import Comboter from './Comboter/Comboter';
import useCombo from './ComboObject/useCombo';
import useComboGenerator from './ComboObject/useComboGenerator';
import { ComboProps } from './ComboObject/types';
import { initCombos } from './ComboObject/initCombos';

const StratagemHell: FunctionComponent = function () {
    const generate: boolean = true;
    // Use the custom hook to generate combos
    const generatedCombos = useComboGenerator({
        numCombos: 5,
        minComboLength: 3,
        maxComboLength: 6,
    });

    console.debug('generatedCombos: ', generatedCombos);

    let combos: Array<ComboProps> = initCombos;

    if (generate) {
        combos = generatedCombos;
    }

    // Use the useCombo hook to manage game state
    const { currentCombo, validateKeyPress, isGameOver, restartGame } = useCombo(combos);
    return (
        <Box
            sx={{
                display: 'flex',
                flexDirection: 'column',
                height: '100vh',
                alignItems: 'center',
                justifyContent: 'space-around',
            }}
        >
            {/* Top Half */}
            <Card
                sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    height: '50vh',
                    width: '80vw',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <Dashboard
                    score={100}
                    timeRemaining={45}
                    nextCombo={['up', 'down']}
                />
            </Card>

            {/* Bottom Half */}
            <Card
                sx={{
                    display: 'flex',
                    flexDirection: 'row',
                    height: '50vh',
                    width: '80vw',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <Comboter
                    currentCombo={currentCombo}
                    validateKeyPress={validateKeyPress}
                    isGameOver={isGameOver}
                    restartGame={restartGame}
                />
            </Card>
        </Box>
    );
};

export default StratagemHell;
