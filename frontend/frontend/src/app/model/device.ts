export interface Device{
    _measurement:string,
    _time: Date,
    _value:string,
    name:string,
    runs_on:string,
    simulated:boolean

}
export interface RgbColor{
    colorName:string,
    colorValue:string
}