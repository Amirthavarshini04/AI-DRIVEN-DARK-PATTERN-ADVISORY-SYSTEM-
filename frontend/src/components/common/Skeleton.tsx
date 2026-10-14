import React from 'react';

export const Skeleton: React.FC<{ className?: string }> = ({ className = "h-4 bg-slate-800/60 rounded-xl" }) => {
  return <div className={`animate-pulse ${className}`} />;
};
