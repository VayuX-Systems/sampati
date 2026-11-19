// Mock API utility functions

export interface MockResponse<T> {
  data: T;
  status: number;
  message: string;
}

export interface MockQueryParams {
  search?: string;
  status?: string;
  category?: string;
  page?: number;
  limit?: number;
  sortBy?: string;
  order?: 'asc' | 'desc';
}

// Simulate network delay
export const mockDelay = (ms: number = 300): Promise<void> => {
  return new Promise(resolve => setTimeout(resolve, ms));
};

// Create mock response wrapper
export const createMockResponse = async <T>(
  data: T,
  status: number = 200,
  message: string = 'Success'
): Promise<MockResponse<T>> => {
  await mockDelay();
  return { data, status, message };
};

// Filter data by search query
export const filterBySearch = <T extends { name?: string; title?: string; description?: string }>(
  data: T[],
  search: string
): T[] => {
  if (!search) return data;
  const searchLower = search.toLowerCase();
  return data.filter(item =>
    (item.name && item.name.toLowerCase().includes(searchLower)) ||
    (item.title && item.title.toLowerCase().includes(searchLower)) ||
    (item.description && item.description.toLowerCase().includes(searchLower))
  );
};

// Filter data by status
export const filterByStatus = <T extends { status?: string }>(
  data: T[] | T | undefined,
  status: string
): T[] => {
  if (!status) return Array.isArray(data) ? data : [];
  if (!data) return [];
  const items = Array.isArray(data) ? data : [data];
  return items.filter(item => item.status === status);
};

// Filter data by category
export const filterByCategory = <T extends { category?: string }>(
  data: T[] | T | undefined,
  category: string
): T[] => {
  if (!category) return Array.isArray(data) ? data : [];
  if (!data) return [];
  const items = Array.isArray(data) ? data : [data];
  return items.filter(item => item.category === category);
};

// Sort data by key
export const sortData = <T extends Record<string, any>>(
  data: T[],
  sortBy: string,
  order: 'asc' | 'desc' = 'asc'
): T[] => {
  if (!sortBy) return data;
  return [...data].sort((a, b) => {
    const aVal = a[sortBy];
    const bVal = b[sortBy];
    if (aVal === undefined) return 1;
    if (bVal === undefined) return -1;
    if (typeof aVal === 'string' && typeof bVal === 'string') {
      return order === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
    }
    if (aVal < bVal) return order === 'asc' ? -1 : 1;
    if (aVal > bVal) return order === 'asc' ? 1 : -1;
    return 0;
  });
};

// Paginate data
export const paginateData = <T>(
  data: T[],
  page: number = 1,
  limit: number = 10
): { items: T[]; total: number; totalPages: number } => {
  const start = (page - 1) * limit;
  const items = data.slice(start, start + limit);
  const total = data.length;
  const totalPages = Math.ceil(total / limit);
  return { items, total, totalPages };
};

// Mock fetch function for API calls
export const mockFetch = async <T>(
  data: T,
  delay: number = 300,
  status: number = 200
): Promise<MockResponse<T>> => {
  await mockDelay(delay);

  // Simulate occasional errors
  if (Math.random() < 0.05) {
    throw new Error('Network error - please try again');
  }

  return createMockResponse(data, status);
};

// Transform mock data for API response
export const mockApi = {
  get: async <T>(
    data: T[],
    params?: MockQueryParams
  ): Promise<{ data: T[]; total: number; totalPages: number }> => {
    let result = data;

    // Apply filters
    if (params?.search) {
      result = filterBySearch(result, params.search);
    }

    // Apply pagination
    const page = params?.page || 1;
    const limit = params?.limit || 10;
    const paginated = paginateData(result, page, limit);

    return {
      data: paginated.items,
      total: paginated.total,
      totalPages: paginated.totalPages,
    };
  },

  getById: async <T extends { id: string }>(
    data: T[],
    id: string
  ): Promise<T | null> => {
    await mockDelay();
    return data.find(item => item.id === id) || null;
  },

  post: async <T>(
    newItem: Omit<T, 'id' | 'createdAt' | 'updatedAt'>,
    data: T[]
  ): Promise<T> => {
    await mockDelay();
    const item = {
      ...newItem,
      id: `new_${Date.now()}`,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    } as T;
    return item;
  },

  put: async <T extends { id: string }>(
    id: string,
    updates: Partial<T>,
    data: T[]
  ): Promise<T | null> => {
    await mockDelay();
    const index = data.findIndex(item => item.id === id);
    if (index === -1) return null;
    data[index] = { ...data[index], ...updates, updatedAt: new Date().toISOString() };
    return data[index];
  },

  delete: async <T extends { id: string }>(
    id: string,
    data: T[]
  ): Promise<boolean> => {
    await mockDelay();
    const index = data.findIndex(item => item.id === id);
    if (index === -1) return false;
    data.splice(index, 1);
    return true;
  },
};