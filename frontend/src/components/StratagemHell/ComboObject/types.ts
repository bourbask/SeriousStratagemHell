export type PossibleKeys = 'left' | 'right' | 'up' | 'down';
export type PossibleStatus = 'idle' | 'loading' | 'success' | 'failed';

export type Uuid = {
    id: string;
};

export type Status = {
    status: PossibleStatus;
};

export type KeyProps = { key: PossibleKeys } & Status & Uuid;

export type ComboProps = {
    name: string;
    keys: Array<KeyProps>;
} & Status &
    Uuid;
