export interface Drone {
    id: number;
    name: string;
    type: string;
  }
  
  export interface Task {
    id: number;
    name: string;
    description: string;
    droneId: number;
    isExecuted: boolean;
  }
  
  export interface Image {
    id: number;
    url: string;
  }
  