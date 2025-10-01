export type CapacityLevel = 'green' | 'yellow' | 'red'

export interface ChatSuggestion {
  startDate: string
  endDate: string
}

export interface ChatResponse {
  message: string
  requestId?: string
  capacity?: CapacityLevel
  suggestions?: ChatSuggestion[]
  status?: string
}

