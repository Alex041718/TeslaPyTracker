export interface GraphPoint {
    timestamp: Date;
    price: number;
    text?: string;
    vin: string;
    paint: string; // Couleur de la peinture
}

export interface Meta {
    totalPoints: number;
    normalizedPoints: number;
    year?: number;
    version?: string;
}

export interface Links {
    self: string;
    next?: string;
    prev?: string;
}

export interface GraphData {
    meta: Meta;
    data: GraphPoint[];
    links: Links;
}