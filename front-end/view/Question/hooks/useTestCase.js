import { useState, useMemo } from "react";

const useTestCase = (dataInput) => {
  const [selectedTestCase, setSelectedTestCase] = useState(0);

  const testCases = useMemo(() => {
    return dataInput?.example_testcase_List?.[0]?.split("\n") || [];
  }, [dataInput]);

  const metaData = useMemo(() => {
    return dataInput?.meta_data ? JSON.parse(dataInput.meta_data) : null;
  }, [dataInput]);

  const paramCount = useMemo(() => {
    return metaData?.params?.length || 0;
  }, [metaData]);

  return {
    selectedTestCase,
    setSelectedTestCase,
    testCases,
    metaData,
    paramCount
  };
};

export default useTestCase;
