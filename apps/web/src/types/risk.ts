export type RiskStatus = 'open' | 'mitigation-planned' | 'in-progress' | 'mitigated' | 'closed' | 'accepted' | 'transferred';

export type Probability = 'rare' | 'unlikely' | 'possible' | 'likely' | 'almost-certain';

export type Impact = 'none' | 'minor' | 'moderate' | 'major' | 'critical';

export interface Risk {
  id: string;
  name: string;
  description: string;
  category: string;
  probability: Probability;
  impact: Impact;
  probabilityScore: number;
  impactScore: number;
  riskScore: number;
  riskLevel: 'low' | 'medium' | 'high' | 'critical';
  status: RiskStatus;
  ownerId: string;
  evidenceId?: string;
  mitigationPlan?: string;
  startDate?: string;
  assessmentDate?: string;
  nextReviewDate?: string;
  createdAt: string;
  updatedAt: string;
}

export interface RiskHeatMapCell {
  probability: Probability;
  impact: Impact;
  count: number;
  risks: Risk[];
}

export interface RiskAnalytics {
  totalRisks: number;
  byRiskLevel: Record<'low' | 'medium' | 'high' | 'critical', number>;
  byStatus: Record<RiskStatus, number>;
  byCategory: Record<string, number>;
  heatMap: RiskHeatMapCell[];
  topRisks: Risk[];
  averageRiskScore: number;
}

export interface RiskSearchParams {
  search?: string;
  status?: RiskStatus;
  riskLevel?: 'low' | 'medium' | 'high' | 'critical';
  category?: string;
  ownerId?: string;
  dateFrom?: string;
  dateTo?: string;
  sortBy?: keyof Risk;
  sortOrder?: 'asc' | 'desc';
  limit?: number;
  offset?: number;
}