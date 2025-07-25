export interface SalePoint {
    date: string;
    sales_count: number;
    sold_vins: string[];
}

export interface SalesData {
    data: SalePoint[];
}